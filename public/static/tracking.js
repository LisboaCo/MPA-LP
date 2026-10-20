/* Tracking base — MPA Advogados. Eventos: page_view (auto) e click_cta (via trackCTA).
   Cada LP declara o próprio trackCTA e empurra page_view/click_cta/lead_submit no dataLayer,
   então aqui só garantimos que o dataLayer exista antes do GTM. */
(function(){
  try{ window.dataLayer = window.dataLayer || []; }catch(e){}
})();
