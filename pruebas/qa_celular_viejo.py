import asyncio, os
from playwright.async_api import async_playwright
F='file://'+os.path.abspath('para-liliana.html')
OLD="""Object.defineProperty(navigator,'deviceMemory',{get:function(){return 2}});Object.defineProperty(navigator,'hardwareConcurrency',{get:function(){return 4}});
window.__long=[];try{new PerformanceObserver(function(l){l.getEntries().forEach(function(e){window.__long.push([Math.round(e.startTime),Math.round(e.duration)])})}).observe({type:'longtask',buffered:true})}catch(e){}"""
FAST="""Object.defineProperty(window,'CARTA',{configurable:true,set:function(v){v.velocidad=VEL;this.__c=v},get:function(){return this.__c}});"""
R=[]
def ok(n,c,i=''): R.append(c); print(('PASS ' if c else 'FAIL ')+n, i)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in ((320,568),(360,640),(412,840)):
            ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2,has_touch=True,is_mobile=True)
            pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
            await pg.add_init_script(OLD); await pg.goto(F); await pg.wait_for_timeout(600)
            await pg.tap('.btn'); await pg.wait_for_timeout(3000); await pg.tap('.controles button:nth-child(2)'); await pg.wait_for_timeout(1500)
            sw=await pg.evaluate('document.documentElement.scrollWidth'); ok(f'{w}px sin scroll horizontal', sw<=w, sw)
            ok(f'{w}px sin errores', not errs, errs[:2]); await ctx.close()
        # old phone: CPU x4 slower, full natural run
        ctx=await b.new_context(viewport={'width':360,'height':640},device_scale_factor=2,has_touch=True,is_mobile=True)
        pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        cdp=await ctx.new_cdp_session(pg); await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
        await pg.add_init_script(OLD+FAST.replace('VEL','5')); await pg.goto(F); await pg.wait_for_timeout(800)
        cls=await pg.evaluate('document.documentElement.className')
        ok('modo liviano y letra grande activos', 'liviano' in cls and 'letra-grande' in cls, cls)
        t0=await pg.evaluate('performance.now()')
        await pg.tap('.btn'); t=0; off=0; n=0
        while t<240000:
            await pg.wait_for_timeout(1000); t+=1000
            r=await pg.evaluate("(()=>{var p=document.querySelector('.pluma');return {fin:!document.querySelector('.fin').hidden, top:p&&p.parentNode?p.getBoundingClientRect().top:null, tit:!!(p&&p.closest&&p.closest('.hitos-tit,.regalos-tit'))}})()")
            if r['top'] is not None and not r['tit']: n+=1;
            if r['top'] is not None and not r['tit']: off+= (r['top']<-5 or r['top']>640)
            if r['fin']: break
        ok('celular viejo (CPU x4): recorrido completo', r['fin'], f'{t//1000}s')
        ok('celular viejo: el texto sigue a la vista', off<=2, f'{off}/{n}')
        lt=await pg.evaluate('window.__long'); ok('celular viejo: lectura fluida (nada >150 ms después de abrir)', not [d for s_,d in lt if s_>t0+4000 and d>150], max([d for s_,d in lt if s_>t0+4000] or [0]))
        hv=await pg.evaluate("document.querySelectorAll('.hito.on').length"); ok('8 fechas en la línea de tiempo', hv==8, hv)
        cf=await pg.evaluate("[].map.call(document.querySelectorAll('.cifra b'),function(b){return b.textContent}).join(',')"); ok('cifras 4,10,2,85', cf=='4,10,2,85', cf)
        imgs=await pg.evaluate("[].map.call(document.querySelectorAll('.reg-foto'),function(i){return i.naturalWidth>0})"); ok('fotos de tarjetas cargadas (5)', len(imgs)==5 and all(imgs), imgs)
        hf=await pg.evaluate("[].map.call(document.querySelectorAll('.hitos-foto img,.hito-foto'),function(i){return i.naturalWidth>0})"); ok('foto de apertura + 2 fotos en fechas', len(hf)==3 and all(hf), hf)
        de=await pg.evaluate("document.querySelector('.firma').innerText"); ok('firma familia Boglione', 'familia Boglione' in de, de)
        cards=await pg.query_selector_all('.regalo'); ok('5 tarjetas (3 locuras + 2 regalos)', len(cards)==5)
        for i,exp in ((1,'4.000'),(2,'queda en Ámsterdam'),(3,'Chofer con flores')):
            await cards[i].scroll_into_view_if_needed(); await cards[i].tap(); await pg.wait_for_timeout(900)
            txt=await cards[i].inner_text(); ok(f'tarjeta {i} se da vuelta', await cards[i].get_attribute('aria-pressed')=='true' and exp in txt)
        ok('celular viejo: sin errores', not errs, errs[:2])
        for sel,name in (('.hitos','lili-hitos'),('.regalos','lili-locuras')):
            y=await pg.evaluate(f"document.querySelector('{sel}').getBoundingClientRect().top+scrollY"); await pg.evaluate(f'scrollTo(0,{y}-140)'); await pg.wait_for_timeout(500); await pg.screenshot(path=name+'.png')
        await cards[3].scroll_into_view_if_needed(); await pg.wait_for_timeout(500); await pg.screenshot(path='lili-uber.png')
        await ctx.close(); await b.close()
    print(f'\n{sum(R)}/{len(R)} OK')
asyncio.run(main())
