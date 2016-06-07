var before;
var now;
var elapsedTime;
var startingTime

function display( notifier, str )
{
    document.getElementById( notifier ).innerHTML = str;
}
function test(){
  alert('gaeafefa');
}

function toMinuteAndSecond( x )
{
    var hour = Math.floor(x / 3600);
    var minutes = Math.floor(x / 60 - (hour * 60))
    var seconds = (x - (minutes * 60) - (hour *3600));

    if(hour < 10)
        hour = '0' + hour;
    if(minutes < 10)
        minutes = '0' + minutes;
    if(seconds < 10)
        seconds = '0' + seconds;

    return hour + ":" + minutes + ":" + seconds;
}

function toHourAndMinute( x )
{
    var hour = Math.floor(x / 60);
    var minutes = x % 60;

    if(minutes < 10)
        minutes = '0' + minutes;

    return hour + ":" + minutes;
}

function setTimer( remain, actions )
{
    ( function countdown()
    {
        display( 'countdown', toMinuteAndSecond( remain ) );
        actions[remain] && actions[remain]();
        //(remain += 1) >= 0 && setTimeout( arguments.callee, 1000 );
        now = new Date();
        elapsedTime = ((now.getTime() - before.getTime()));
        if(((elapsedTime/1000) + startingTime) > remain){
        //Recover the time lost while inactive.
            remain += (Math.floor(elapsedTime/1000)-remain+startingTime+1);
        }
        else{
            remain++;
        }
        remain >= 0 && setTimeout( arguments.callee, 1000 );
    })();
}
function runClock(begin) {
    startingTime = begin;
    before = new Date();
    setTimer( begin, {
        2: function()
        {
            display( 'notifier', 'seconds');
        },
        1: function()
        {
            display( 'notifier', 'second');
        },
        0: function()
        { 
            display( 'notifier', 'seconds');
        }
        } 
    );
}
