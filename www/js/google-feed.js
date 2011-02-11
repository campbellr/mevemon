google.load("feeds", "1");

function nl2p(text) {
  text = escape(text);
  if(text.indexOf('%0D%0A') > -1) {
    re_nlchar = /%0D%0A/g;
  } else if (
    text.indexOf('%0A') > -1) {
      re_nlchar = /%0A/g ;
  } else if (
    text.indexOf('%0D') > -1) {
    re_nlchar = /%0D/g ;
  } else { return unescape(text); }
  return unescape( text.replace(re_nlchar,'</p><p>') );
}

function first_paragraph(ptext) {

  pindex = ptext.indexOf("\n\n");
  if ( pindex < 100 ) {
    pindex = ptext.indexOf("\n\n", pindex + 1);
  }

  paragraph = ptext.slice(0, pindex);

  return paragraph;

}

function initialize() {
  var feed = new google.feeds.Feed("https://garage.maemo.org/export/rss_sfnews.php?group_id=1544");
  feed.setNumEntries(4);
  feed.load(function(result) {

  var container = document.getElementById("garage_feed");

  if (!result.error) {
    for (var i = 0; i < result.feed.entries.length; i++) {
      var entry = result.feed.entries[i];
      var div = document.createElement("div");
      final_content = nl2p(first_paragraph(entry.content));
      final_content = final_content + " <a href=\"" + entry.link + "\">(Read more)</a>";
      div.innerHTML = "<p><h3><a href=\"" + entry.link + "\">" + entry.title + "</a></h3></p><p><b>Posted by " + entry.author + " on " + entry.publishedDate  + "</b></p><p></p><p>" + final_content + "</p>";
      container.appendChild(div);
    }
  } else { container.innerHTML = "<p><h3>Error loading news feed.</h3></p>"; }
  });
}

google.setOnLoadCallback(initialize);
