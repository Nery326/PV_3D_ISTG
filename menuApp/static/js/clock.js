const time = document.getElementById("time");
const day = document.getElementById("date");
function getCurrentDate(){
             const currentDate = new Date(),
                 options = {
                 weekday: 'short', year: 'numeric', month: 'long', day: 'numeric'
                 }
                 date.innerHTML = currentDate.toLocaleDateString('es',options)
         }
function getCurrentTime(){
    const currentDate =new Date(),
        hours = formatTime(currentDate.getHours()),
        minutes = formatTime(currentDate.getMinutes()),
        seconds = formatTime(currentDate.getSeconds()),
        format = (hours < 12) || (hours == 24) ? 'AM' : 'PM'
    time.innerHTML = `${hours}:${minutes}:${seconds} <small>${format}</small>`
}
function formatTime(value){
    return value < 10 ? `0${value}`: value
}
getCurrentDate()
setInterval(getCurrentTime, 1000)
