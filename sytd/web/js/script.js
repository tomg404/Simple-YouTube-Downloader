// starts pythons download function with url parameter
function start_download(){
  let url = document.getElementById('url-field').value;
  console.log("downloading video: " + url);
  eel.download(url);
}

// opens directory selection window
async function open_dir_browser() {
  var download_path = await eel.open_dir_browser()();
    if (download_path) {
      console.log(download_path);
    }
}

// get video_id from url (thanks https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url)
function youtube_url_parser(url){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? match[7] : false;
}

// changes thumbnail (runs every second (not the best solution i know))
function update_thumbnail() {
  let url = document.getElementById('url-field').value;
  let video_id = youtube_url_parser(url);
  let picture_url = 'img/noinput.svg';
  if(video_id != false) {
    picture_url = 'https://img.youtube.com/vi/' + video_id + '/0.jpg';
  }
  document.getElementById('video-thumbnail').src = picture_url;
}

// update progress bar via python backend
eel.expose(update_progressbar);
function update_progressbar(percentage) {
  let pb = document.getElementById('progress_bar0');
  pb.style.width = percentage.toString() + "%";
  pb.innerHTML = percentage.toString() + "%";
}

// reset progress bar
function reset_progressbar() {
  let pb = document.getElementById('progress_bar0');
  pb.style.width = "0%"
  pb.innerHTML = "";
}

// update status field
eel.expose(update_status);
function update_status(msg) {
  document.getElementById('status-field').value = "[Status] " + msg;
}

// update version text of the version badge
eel.expose(update_version_badge)
function update_version_badge(version) {
  document.getElementById('version-badge').innerHTML = version;
}
