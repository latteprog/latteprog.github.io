function fileExists(url) {
    if(url)
    {
        var req = new XMLHttpRequest();
        req.open('GET', url, false);
        req.send();
        return (req.status == 200);
    } else {
        return false;
    }
}

function createLoadPostSynopsisCallback(postId)
{
	return function(obj) {
		$("#post" + postId).append("<div class='postLeftColumn' id='postLeftColumn" + postId + "'></div>");
		$("#post" + postId).append("<div class='postRightColumn' id='postRightColumn" + postId + "'></div>");
		$("#post" + postId).append("<div style='clear: both;'></div>");

		$("#postRightColumn" + postId).click(function() {
			window.history.pushState({ state: window.currState }, $(this).attr('title'), $(this).attr('href'));
			loadPost(obj.id);
		});

		$("#postLeftColumn" + postId).append("<a href='javascript:sharePopup(\"" + obj.facebookShareLink + "\")'><img src='assets/facebookShare.png' style='width: 45%; cursor: pointer;'></a><br style='line-height: 170%'>");
		$("#postLeftColumn" + postId).append("<a href='javascript:sharePopup(\"" + obj.twitterShareLink + "\")'><img src='assets/twitterShare.png' style='width: 45%; cursor: pointer;'></a>");

		$("#postRightColumn" + postId).append("<div class='postTitle'><b>" + obj.title + "</b>&#09;<font size='4' color='#999999'>-&#09;" + obj.date + "</font></div>");
		$("#postRightColumn" + postId).append("<div class='postSynopsis'>" + obj.synopsis + "</div>");
	};
}

function loadPost(id) {
	if(!fileExists("html/articles/" + id + ".html"))
	{
		loadHome();
		return;
	}

	$("#content").empty();

	$("#content").append("<div class='post' id='post'></div>");

	$("#post").append("<div class='postLeftColumn' id='postLeftColumn'></div>");
	$("#post").append("<div class='postRightColumn' id='postRightColumn'></div>");
	$("#post").append("<div style='clear: both;'></div>");

	$("#postRightColumn").css("cursor", "default");

	$.getJSON("json/articles/" + id + ".json", function(obj) {
		document.title = obj.title;
		$("#postLeftColumn").append("<a href='javascript:sharePopup(\"" + obj.facebookShareLink + "\")'><img src='assets/facebookShare.png' style='width: 45%;'></a><br style='line-height: 170%'>");
		$("#postLeftColumn").append("<a href='javascript:sharePopup(\"" + obj.twitterShareLink + "\")'><img src='assets/twitterShare.png' style='width: 45%;'></a>");
	});

	$("#postRightColumn").load("html/articles/" + id + ".html");

	window.currState = id;
}

function loadHeader() {
	$("<div id='header'></div>").hide().appendTo("#container").fadeIn(800);
	$("<div id='content'></div>").hide().appendTo("#container").fadeIn(800);
	$("#header").append("<img id='homeBanner' src='assets/homeBanner.png' style='height: 60%; position: absolute; top: 20%; left: 15%; cursor: pointer;'>");

	$("#homeBanner").click(function() {
		window.history.pushState({ state: window.currState }, $(this).attr('title'), $(this).attr('href'));
		loadHome();
	});

	$("#header").append("<hr style='clear: both; background-color: #000000; width: 80%; position: absolute; bottom: 0px; left: 10%; border-top: #999999 solid 1px;'>");
	//$("#header").append("<input type='text' id='searchBox' style='width: 20%; position: absolute; top: 50%; right: 16%; font-family: CSChatThai; font-size: 18px; background: url(\"assets/searchLogo.png\") top right no-repeat;'>")
}

function loadHome() {
	if($("#container").has("#header").length == 0)
	{
		loadHeader();
	} else {
		$("#content").empty();
	}

	document.title = "latteprog.github.io";
	window.currState = "home";

	$("#content").append("<div id='mainContent'></div>")
	$("#content").append("<div id='sideBar'></div>");

	$("#sideBar").append("<span style='font-family: CSChatThai; font-size: 24px; color: #C62818;'><b>Neighbours</b><br style='line-height: 200%;'></span>");
	$("#sideBar").append("<a href='https://www.magkun.com/' target='_blank'><img src='/assets/magkun.png' width='80%'></a>");
	$("#sideBar").append("<br style='line-height: 280%;'><span style='font-family: CSChatThai; font-size: 24px; color: #C62818;'><b>Contact</b><br style='line-height: 200%;'></span>");
	$("#sideBar").append("<span style='font-family: CSChatThai; font-size: 20px; color: #C62818;'>Twitter: <a href='https://twitter.com/latteprog1'><span style='color: #000000;' target='_blank'>@latteprog1</span></a><br style='line-height: 200%;'></span>");

	$.getJSON("json/topics.json", function(obj) {
		for(var i = 0; i < obj.topicsList.length; i++)
		{
			$("#mainContent").append("<div class='post' id='post" + (i + 1) + "'></div>");
		}

		for(var i = 0; i < obj.topicsList.length; i++)
		{
			$.getJSON("json/articles/" + obj.topicsList[i] + ".json", createLoadPostSynopsisCallback(i + 1));
		}
	});
}

function loadSplashScreen(nextPage) {
	$("#container").append("<img id='splashScreenLogo' src='assets/splashScreenLogo.png' style='visibility: hidden;'>");
	$("#container").append("<div id='splashScreenText' style='visibility: hidden;'>สวัสดีครับ ผมลาเต้ครับ ตอนนี้กำลังเรียนวิทยาการคอมพิวเตอร์อยู่ระดับปริญญาตรี ในบล็อกนี้ผมจะเขียนเล่าเรื่องเกี่ยวกับคอมพิวเตอร์และคณิตศาสตร์ ฝากเนื้อฝากตัวด้วยนะครับ ^_^</div>");
	$("#container").append("<img id='splashScreenButton' src='assets/splashScreenButton.png' style='visibility: hidden;'>");
	window.splashScreenInt = window.setInterval(function() {
		c = Math.min($(document).width() / 1366, $(document).height() / 667);

		$("#splashScreenLogo").css("width", (c * 484) + "px");
		$("#splashScreenLogo").css("height", (c * 404) + "px");
		$("#splashScreenLogo").css("top", ($(document).height() - (c * 404)) / 2 + "px");
		$("#splashScreenLogo").css("left", ($(document).width() / 2 - (c * 520)) + "px");

		$("#splashScreenText").css("width", (c * 500) + "px");
		$("#splashScreenText").css("top", ($(document).height() - (c * 240)) / 2 + "px");
		$("#splashScreenText").css("left", ($(document).width() / 2 + (c * 50)) + "px");
		$("#splashScreenText").css("font-size", (c * 24) + "px");

		$("#splashScreenButton").css("width", (c * 336) + "px");
		$("#splashScreenButton").css("height", (c * 56) + "px");
		$("#splashScreenButton").css("left", ($(document).width() / 2 + (c * 130)) + "px");
		$("#splashScreenButton").css("top", ($(document).height() + (c * 100)) / 2 + "px");

		$("#splashScreenText").css("visibility", "visible");
		$("#splashScreenLogo").css("visibility", "visible");
		$("#splashScreenButton").css("visibility", "visible");
	}, 30);

	$("#splashScreenButton").click(function() {
		window.clearInterval(splashScreenInt);
		$("#splashScreenLogo").fadeOut(800, function() {
			$("#container").remove("#splashScreenLogo");
		});

		$("#splashScreenText").fadeOut(800, function() {
			$("#container").remove("#splashScreenText");
		});

		$("#splashScreenButton").fadeOut(800, function() {
			$("#container").remove("#splashScreenButton");
		});

		localStorage.setItem("visitedPage", "true");

		if(nextPage == "home")
		{
			loadHome();
		} else {
			loadHeader();
			loadPost(nextPage);
		}
	});
}

function parseParameter(args, attr)
{
	items = args.split("&");

	for(var i = 0; i < items.length; i++)
	{
		pair = items[i].split("=");

		if(pair[0] == "post")
		{
			return pair[1];
		}
	}

	return "";
}

function sharePopup(url)
{
	window.open(url, "Share", "status = 1, height = 250, width = 360, resizable = 0")
}

window.onpopstate = function(e) {
	if(!e.state)
	{
		loadHome();
		return;
	}

	if(e.state.state == "home")
	{
		loadHome();
	} else {
		loadPost(e.state.state);
	}
}