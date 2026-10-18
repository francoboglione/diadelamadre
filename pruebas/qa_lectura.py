"""Pruebas de lectura: la persona frena, sube, baja o toca, y la carta no se rompe.
Uso: python3 pruebas/qa_lectura.py carta-armada.html [otra.html ...]  (necesita Playwright)"""
import asyncio, os, random, sys
from playwright.async_api import async_playwright

FAST = """Object.defineProperty(window,'CARTA',{configurable:true,set:function(v){v.velocidad=VEL;this.__c=v},get:function(){return this.__c}});"""
JS_ESTADO = """(()=>{var c=window.__carta&&window.__carta.cursor(),b=document.querySelector('.controles button'),v=document.querySelector('.volver');
 var r=c&&c.parentNode?c.getBoundingClientRect():null;
 return {escritas:document.querySelectorAll('.c.t,.on,.pol.ya,.pol.vuela').length, faltan:document.querySelectorAll('.c:not(.t)').length,
   fin:!document.querySelector('.fin').hidden, top:r?r.top:null, y:scrollY, alto:innerHeight,
   boton:b?b.innerText.trim():'', volver:v&&!v.hidden?v.innerText.trim():''}})()"""

class QA:
    def __init__(s, nombre): s.n=nombre; s.r=[]
    def ok(s, t, c, info=''):
        s.r.append(bool(c)); print(('  PASS ' if c else '  FAIL ')+t, info)

async def abrir(b, archivo, vel):
    ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = await ctx.new_page(); errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.add_init_script(FAST.replace('VEL', str(vel)))
    await pg.goto('file://'+os.path.abspath(archivo)); await pg.wait_for_timeout(700)
    cdp = await ctx.new_cdp_session(pg)
    await pg.tap('.btn'); await pg.wait_for_timeout(4500)
    return ctx, pg, cdp, errs

async def deslizar(cdp, dy, vel=1400, pg=None):
    # dedo real: toca, arrastra en pasos (la página se mueve con él) y suelta.
    # dy > 0: el dedo baja y la página sube (releer); dy < 0: adelantarse
    pasos = 10
    await cdp.send('Input.dispatchTouchEvent', {'type':'touchStart','touchPoints':[{'x':200,'y':420}]})
    for i in range(1, pasos+1):
        y = max(5, min(835, 420 + dy*i/pasos*0.25))
        await cdp.send('Input.dispatchTouchEvent', {'type':'touchMove','touchPoints':[{'x':200,'y':y}]})
        await cdp.send('Runtime.evaluate', {'expression':'window.scrollBy(0,%d)' % int(-dy/pasos)})
        await asyncio.sleep(max(0.012, abs(dy)/vel/pasos))
    await cdp.send('Input.dispatchTouchEvent', {'type':'touchEnd','touchPoints':[]})

async def estado(pg): return await pg.evaluate(JS_ESTADO)

async def correr(archivo):
    q = QA(archivo); print('\n== '+os.path.basename(archivo))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # A) sube a releer: se frena, aparece "Seguir leyendo", al tocarlo vuelve y sigue
        ctx,pg,cdp,errs = await abrir(b, archivo, 1.5)
        await pg.wait_for_timeout(9000)
        await deslizar(cdp, 1200); await pg.wait_for_timeout(1500)
        e1 = await estado(pg); await pg.wait_for_timeout(2000); e2 = await estado(pg)
        q.ok('A1 al subir a releer, la escritura espera', e2['escritas']==e1['escritas'], f"{e1['escritas']}->{e2['escritas']}")
        q.ok('A2 aparece "↓ Seguir leyendo"', 'Seguir leyendo' in e2['volver'], e2['volver'])
        q.ok('A3 no la arrastra mientras relee', abs(e2['y']-e1['y'])<5, f"{e1['y']}->{e2['y']}")
        await pg.tap('.volver'); await pg.wait_for_timeout(2500); e3 = await estado(pg)
        q.ok('A4 al tocarlo vuelve a la pluma', e3['top'] is not None and -200 <= e3['top'] <= e3['alto'], e3['top'])
        await pg.wait_for_timeout(3000); e4 = await estado(pg)
        q.ok('A5 y sigue escribiendo', e4['escritas']>e3['escritas'] and e4['volver']=='' and 'Pausar' in e4['boton'], f"{e3['escritas']}->{e4['escritas']} {e4['boton']}")
        # B) sube y vuelve sola con el dedo: retoma sin tocar nada
        y0 = (await estado(pg))['y']
        await deslizar(cdp, 900); await pg.wait_for_timeout(1500)
        y1 = (await estado(pg))['y']
        await deslizar(cdp, -(y0-y1)); await pg.wait_for_timeout(3500); e5 = await estado(pg)
        await pg.wait_for_timeout(3000); e6 = await estado(pg)
        q.ok('B1 al volver con el dedo, retoma sola', e6['escritas']>e5['escritas'] and 'Pausar' in e6['boton'], f"{e5['escritas']}->{e6['escritas']} {e6['boton']}")
        # C) se adelanta hacia abajo: espera y ofrece "Volver a donde iba"
        await deslizar(cdp, -2500, 3000); await pg.wait_for_timeout(1800); c1 = await estado(pg)
        await pg.wait_for_timeout(1500); c2 = await estado(pg)
        if c1['top'] is not None and c1['top'] < 0:
            q.ok('C1 adelantada: la escritura espera', c2['escritas']==c1['escritas'], f"{c1['escritas']}->{c2['escritas']}")
            q.ok('C2 aparece "↑ Volver a donde iba"', 'Volver a donde iba' in c2['volver'], c2['volver'])
            await pg.tap('.volver'); await pg.wait_for_timeout(2500); c3 = await estado(pg)
            q.ok('C3 sube hasta la pluma', c3['top'] is not None and -200 <= c3['top'] <= c3['alto'], c3['top'])
        else:
            q.ok('C0 no había más carta abajo para adelantarse (página corta)', True, c1['top'])
        # D) Pausar real con el dedo, moverse, Seguir
        await pg.tap('.controles button:nth-child(1)'); d1 = await estado(pg)
        await deslizar(cdp, 700); await pg.wait_for_timeout(2500); d2 = await estado(pg)
        q.ok('D1 Pausar frena aunque se mueva', d2['escritas']==d1['escritas'] and 'Seguir' in d2['boton'], f"{d1['escritas']}->{d2['escritas']} {d2['boton']}")
        await pg.tap('.controles button:nth-child(1)'); await pg.wait_for_timeout(2500); d3 = await estado(pg)
        q.ok('D2 Seguir vuelve a la pluma y escribe', d3['escritas']>d2['escritas'] and d3['top'] is not None and -200 <= d3['top'] <= d3['alto'], f"top={d3['top']}")
        # E) un toque suelto sobre el texto no la rompe
        await pg.touchscreen.tap(200, 300); await pg.wait_for_timeout(3000); e7 = await estado(pg)
        q.ok('E1 un toque suelto: retoma sola', 'Pausar' in e7['boton'] and e7['volver']=='', e7['boton'])
        for k in range(3):
            await pg.wait_for_timeout(2500 + k*1700); await pg.touchscreen.tap(120 + k*60, 260 + k*120)
            await pg.wait_for_timeout(3200); ek = await estado(pg)
            q.ok(f'E{3+k} toque suelto #{k+1} en otro momento: no se queda trabada', 'Pausar' in ek['boton'] and ek['volver']=='', ek['boton'])
        q.ok('E2 sin errores', not errs, errs[:2]); await ctx.close()

        # F) estrés: 25 gestos al azar, después Seguir; tiene que terminar completa
        ctx,pg,cdp,errs = await abrir(b, archivo, 6)
        random.seed(7)
        for i in range(25):
            a = random.choice(['arriba','abajo','toque','pausa','tarjeta'])
            try:
                if a=='arriba': await deslizar(cdp, random.randint(200,1500), 2500)
                elif a=='abajo': await deslizar(cdp, -random.randint(200,1500), 2500)
                elif a=='toque': await pg.touchscreen.tap(random.randint(60,330), random.randint(150,650))
                elif a=='pausa': await pg.tap('.controles button:nth-child(1)', timeout=1500)
                else:
                    t = await pg.query_selector_all('.regalo.on')
                    if t: await t[random.randrange(len(t))].tap(timeout=1500)
            except Exception: pass
            await pg.wait_for_timeout(random.randint(200,900))
        try: await pg.tap('.volver', timeout=800)
        except Exception: pass
        st = await estado(pg)
        if not st['fin'] and 'Seguir' in st['boton']: await pg.tap('.controles button:nth-child(1)', timeout=3000)
        t=0
        while t < 200000:
            await pg.wait_for_timeout(1000); t+=1000
            st = await estado(pg)
            if st['fin']: break
            if 'Seguir' in st['boton'] or st['volver']:
                try: await pg.tap('.volver' if st['volver'] else '.controles button:nth-child(1)', timeout=800)
                except Exception: pass
        q.ok('F1 después de 25 gestos al azar, termina completa', st['fin'] and st['faltan']==0, f"{t//1000}s faltan={st['faltan']}")
        q.ok('F2 sin errores', not errs, errs[:2])
        ov = await pg.evaluate("getComputedStyle(document.body).overscrollBehaviorY")
        q.ok('G1 bajar desde arriba no recarga la página (Android)', ov=='contain', ov)
        await ctx.close()

        # H) "Ver todo" mientras espera: muestra todo y saca el botón
        ctx,pg,cdp,errs = await abrir(b, archivo, 1.5)
        await pg.wait_for_timeout(6000); await deslizar(cdp, 1500); await pg.wait_for_timeout(1800)
        await pg.tap('.controles button:nth-child(2)'); await pg.wait_for_timeout(1500); h = await estado(pg)
        q.ok('H1 Ver todo mientras relee: carta completa', h['fin'] and h['faltan']==0 and h['volver']=='', h)
        q.ok('H2 sin errores', not errs, errs[:2]); await ctx.close()
        await b.close()
    print(f'  {sum(q.r)}/{len(q.r)} OK'); return all(q.r)

if __name__ == '__main__':
    res = [asyncio.run(correr(a)) for a in sys.argv[1:]]
    sys.exit(0 if all(res) else 1)
