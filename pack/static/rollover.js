$(document).ready(function(){
    let img = $('img'),
        src =  img.attr("src"),
        altSrc = img.attr("data-alt-src");

    img.css({
        "width": img.width(),
        "height": img.height(),
        "display": "block",
        "background": "url("+src+")",
        "transition": "all 0.6s ease-in-out"
    })
    img.attr("src", "");
    img.attr("alt", "");

    img
        .mouseenter(()=>{
            img.css({
                "background": "url("+altSrc+")",
            })
        })
        .mouseleave(()=>{
            img.css({
                "background": "url("+src+")",
            })
        })
})