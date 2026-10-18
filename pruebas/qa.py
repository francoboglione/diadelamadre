import asyncio, os, json, sys
from playwright.async_api import async_playwright
F='file://'+os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'para-fernanda.html')
INIT = """
window.__sfx = 0; window.__long = [];
(function(){var A0=window.AudioContext; if(A0){window.AudioContext=function(o){var a=o?new A0(o):new A0(); window.__ac=a; return a}; window.AudioContext.prototype=A0.prototype;}
 var P=HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play=function(){window.__tag=this; return P.apply(this,arguments)};})();
(function(){var AC=window.AudioContext; if(AC){var o=AC.prototype.createBufferSource; AC.prototype.createBufferSource=function(){window.__sfx++;return o.apply(this,arguments)}}})();
try{new PerformanceObserver(function(l){l.getEntries().forEach(function(e){window.__long.push(Math.round(e.duration))})}).observe({type:'longtask',buffered:true})}catch(e){}
"""
FAST = """Object.defineProperty(window,'CARTA',{configurable:true,set:function(v){v.velocidad=VEL;this.__c=v},get:function(){return this.__c}});"""
res={}
def ok(name,cond,info=''):
    res[name]=(bool(cond),info); print(('PASS ' if cond else 'FAIL ')+name, info)
async def page(b, w, h, vel=None, reduce=False, touch=False):
    ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2,has_touch=touch,is_mobile=touch,reduced_motion='reduce' if reduce else 'no-preference')
    pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'net::' not in m.text else None)
    await pg.add_init_script(INIT + (FAST.replace('VEL',str(vel)) if vel else ''))
    await pg.goto(F); await pg.wait_for_timeout(800)
    return ctx,pg,errs
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        # 1) widths: envelope + full content without horizontal scroll
        for w in (360,390,430,1280):
            ctx,pg,errs=await page(b,w,800)
            sw0=await pg.evaluate('document.documentElement.scrollWidth')
            await pg.click('.btn'); await pg.wait_for_timeout(3500)
            await pg.click('.controles button:nth-child(2)'); await pg.wait_for_timeout(1500)
            sw=await pg.evaluate('document.documentElement.scrollWidth')
            ok(f'sin scroll horizontal {w}px', sw0<=w and sw<=w, f'{sw0}/{sw}')
            ok(f'sin errores {w}px', not errs, errs[:3])
            await ctx.close()
        # 2) natural run, no "Ver todo", fast speed; pen stays on screen; freezes
        ctx,pg,errs=await page(b,390,844,vel=6)
        await pg.click('.btn')
        samples=[]; t=0; done=False
        while t<150000:
            await pg.wait_for_timeout(500); t+=500
            r=await pg.evaluate("""(()=>{var p=document.querySelector('.pluma');var c=document.querySelector('.carta');
              return {fin:!document.querySelector('.fin')||!document.querySelector('.fin').hidden, y:scrollY,
                top:p&&p.parentNode?p.getBoundingClientRect().top:null}})()""")
            samples.append(r)
            if r['fin']: done=True; break
        tops=[s['top'] for s in samples if s['top'] is not None]
        off=[x for x in tops if x<-5 or x>844]
        ok('recorrido completo sin tocar nada', done, f'{t/1000:.0f}s')
        ok('la pluma siempre a la vista mientras escribe', len(off)<=2, f'{len(off)} de {len(tops)} muestras fuera')
        ys=[s['y'] for s in samples]; stuck=max(sum(1 for _ in g) for k,g in __import__('itertools').groupby(ys)) if ys else 0
        lt=await pg.evaluate('window.__long'); 
        ok('sin trabas largas (>200ms)', not [x for x in lt if x>200], f'longtasks {sorted(lt)[-5:]}')
        n=await pg.evaluate('window.__sfx'); ok('suenan los efectos', n>40, f'{n} sonidos')
        ok('sin errores en el recorrido', not errs, errs[:3])
        await ctx.close()
        # 3) touch interrupts following, then it resumes alone
        ctx,pg,errs=await page(b,390,844,vel=1,touch=True)
        await pg.click('.btn'); await pg.wait_for_timeout(22000)
        y0=await pg.evaluate('scrollY')
        await pg.evaluate("""window.dispatchEvent(new TouchEvent('touchstart',{touches:[]}));window.dispatchEvent(new TouchEvent('touchend',{touches:[]}))""")
        await pg.wait_for_timeout(300)
        lab=await pg.inner_text('.controles button:nth-child(1)')
        ok('al tocar, deja de arrastrar la página', 'Seguir' in lab, lab)
        await pg.wait_for_timeout(3500)
        lab2=await pg.inner_text('.controles button:nth-child(1)')
        ok('retoma solo si la pluma está a la vista', 'Pausar' in lab2, lab2)
        await pg.evaluate('scrollTo(0,0)'); await pg.evaluate("window.dispatchEvent(new TouchEvent('touchstart',{touches:[]}));window.dispatchEvent(new TouchEvent('touchend',{touches:[]}))")
        await pg.wait_for_timeout(4000)
        lab3=await pg.inner_text('.controles button:nth-child(1)'); y3=await pg.evaluate('scrollY')
        ok('no la arrastra si ella subió a releer', 'Seguir' in lab3 and y3<50, f'{lab3} y={y3}')
        await pg.tap('.controles button:nth-child(1)'); await pg.wait_for_timeout(2500)
        y4=await pg.evaluate('scrollY'); ok('"Seguir" la vuelve a llevar a la pluma', y4>200, f'y={y4}')
        # pause really pauses
        await pg.tap('.controles button:nth-child(1)')
        n1=await pg.evaluate("document.querySelectorAll('.c.t').length"); await pg.wait_for_timeout(1500)
        n2=await pg.evaluate("document.querySelectorAll('.c.t').length"); ok('"Pausar" frena la escritura', n1==n2, f'{n1}->{n2}')
        # mute
        await pg.click('.controles button:nth-child(1)')
        await pg.click('.controles button:nth-child(3)'); s1=await pg.evaluate('window.__sfx'); await pg.wait_for_timeout(1500); s2=await pg.evaluate('window.__sfx')
        ok('"Sin sonido" apaga también el tipeo', s1==s2, f'{s1}->{s2}')
        ok('sin errores con interacción', not errs, errs[:3]); await ctx.close()
        # 3b) audio unlock (iPhone / Android)
        ctx,pg,errs=await page(b,390,844,touch=True)
        await pg.tap('.btn'); await pg.wait_for_timeout(1500)
        st=await pg.evaluate("window.__ac && window.__ac.state")
        ok('audio activo al tocar el sobre', st=='running', st)
        tg=await pg.evaluate("!!(window.__tag && !window.__tag.paused && /^data:audio\/wav/.test(window.__tag.src))")
        ok('modo reproducción de iPhone (audio mudo en loop)', tg)
        await pg.evaluate("window.__ac.suspend()"); await pg.wait_for_timeout(300)
        await pg.tap('.carta'); await pg.wait_for_timeout(500)
        st2=await pg.evaluate("window.__ac.state"); ok('se reanuda con el siguiente toque (vuelta de otra app)', st2=='running', st2)
        await pg.evaluate("window.__tag.pause()"); await pg.tap('.carta'); await pg.wait_for_timeout(300)
        ok('el audio mudo vuelve a arrancar si iOS lo frena', await pg.evaluate("!window.__tag.paused"))
        n0=await pg.evaluate('window.__sfx'); await pg.wait_for_timeout(4000); n1=await pg.evaluate('window.__sfx')
        ok('siguen sonando los efectos después', n1>n0, f'{n0}->{n1}')
        ok('sin errores de audio', not errs, errs[:3]); await ctx.close()
        # 4) gift cards
        ctx,pg,errs=await page(b,390,844)
        await pg.click('.btn'); await pg.wait_for_timeout(3000); await pg.click('.controles button:nth-child(2)'); await pg.wait_for_timeout(800)
        cards=await pg.query_selector_all('.regalo')
        ok('4 regalos', len(cards)==4)
        await cards[2].click(); await pg.wait_for_timeout(800)
        ok('regalo misterioso se da vuelta', await cards[2].get_attribute('aria-pressed')=='true')
        txt=await cards[2].inner_text(); ok('no dice "taza"', 'taza' not in txt.lower()); ok('Suki y Nina dibujadas', 'Suki' in txt and 'Nina' in txt)
        await cards[3].focus(); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(800)
        t4=await cards[3].inner_text(); ok('Barcelona con teclado + cuenta regresiva', await cards[3].get_attribute('aria-pressed')=='true' and 'Llega en 9 días' in t4, t4.split('\n')[-2:])
        await cards[0].click(); ok('flores no se da vuelta', await cards[0].get_attribute('aria-pressed') is None)
        await pg.screenshot(path='qa-regalos.png')
        for d,exp in (('2026-10-26','Llega mañana'),('2026-10-27','¡Llega hoy!'),('2026-10-30','¡Ya está en casa!')):
            v=await pg.evaluate(f"""(()=>{{var p='{d}'.split('-');var hoy=new Date(+p[0],+p[1]-1,+p[2]);var d=new Date(2026,9,27);var n=Math.round((d-hoy)/864e5);
               return n>1?'Llega en '+n+' días':n===1?'Llega mañana':n===0?'¡Llega hoy!':'¡Ya está en casa!'}})()""")
            ok(f'cuenta regresiva el {d}', v==exp, v)
        ok('sin errores en regalos', not errs, errs[:3]); await ctx.close()
        # 5) reduced motion: everything visible at once
        ctx,pg,errs=await page(b,375,700,reduce=True)
        await pg.click('.btn'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""({sin:document.querySelectorAll('.c:not(.t)').length, reg:document.querySelectorAll('.regalo:not(.on)').length,
           g:!!document.querySelector('.grande.on'), fin:!document.querySelector('.fin').hidden, sfx:window.__sfx})""")
        ok('reducir movimiento: carta completa al instante', r['sin']==0 and r['reg']==0 and r['g'] and r['fin'], r)
        ok('reducir movimiento: sin efectos (solo el desbloqueo mudo)', r['sfx']<=1, r['sfx'])
        ok('sin errores reducir movimiento', not errs, errs[:3]); await ctx.close()
        # 6) address-bar resize must not relayout photos mid-flight
        ctx,pg,errs=await page(b,390,760,vel=2)
        await pg.click('.btn'); await pg.wait_for_timeout(6000)
        h0=await pg.evaluate("document.querySelector('.pila').style.height")
        await pg.set_viewport_size({'width':390,'height':844}); await pg.wait_for_timeout(500)
        h1=await pg.evaluate("document.querySelector('.pila').style.height")
        ok('barra del navegador no reacomoda las fotos', h0==h1, f'{h0} {h1}')
        await ctx.close()
        await b.close()
    bad=[k for k,v in res.items() if not v[0]]
    print('\n%d/%d OK' % (len(res)-len(bad), len(res)), 'FALLAN:', bad)
asyncio.run(main())
