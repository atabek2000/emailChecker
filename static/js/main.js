function htmlspecialchars_decode(text){
    text = text.replaceAll("&amp;", "&")
    text = text.replaceAll("&gt;", ">")
    text = text.replaceAll("&lt;", "<")
    text = text.replaceAll("&quot;", '\"')
    return text
}