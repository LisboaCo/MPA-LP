import{a as c}from"./EwDkLrRW.js";function m(){c({link:[{key:"intl-tel-input-css",rel:"stylesheet",href:"https://stcdn.leadconnectorhq.com/intl-tel-input/17.0.12/css/intlTelInput.min.css"}],script:[{key:"libphonenumber-js",src:"https://stcdn.leadconnectorhq.com/libphonenumber/1.12.41/libphonenumber-js.min.js",async:!0,type:"text/javascript"},{key:"intl-tel-input-utils",src:"https://stcdn.leadconnectorhq.com/intl-tel-input/17.0.12/js/utils.min.js",async:!0,type:"text/javascript"},{key:"intl-tel-input-js",src:"https://stcdn.leadconnectorhq.com/intl-tel-input/intlTelInput.min.js",async:!0,type:"text/javascript"}]})}const u=(e,t)=>{const o=e?.bgImage?.trim()||"",n=e?.mobileBgImage?.trim()||"",s=!!e?.mobileBgImageDeleted;return n||(s?"":o)},a=(e,t=!1)=>e?`background-image: url('${e}')${t?" !important":""};
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
background-position: top center;`:`background-image: none !important;
background-attachment: initial;
background-size: initial;
background-repeat: initial;
background-position: initial;`,g=(e,t)=>{const o=t?.bgImage?.trim?.()||"",n=t?.mobileBgImage?.trim?.()||"",s=t?.mobileBgImageDeleted===!0,r=a(o);let i="";return n?i=a(n,!0):s?i=a(""):i=r,`
${e} {
  ${r}
}
@media screen and (max-width: 1024px) {
  ${e} {
    ${i}
  }
}`};export{g as b,u as g,m as u};
