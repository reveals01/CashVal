function getDaysInMonth(month, year) {
  var date = new Date(year, month, 1);
  var days = [];
  while (date.getMonth() === month) {
    days.push(new Date(date));
    date.setDate(date.getDate() + 1);
  }
  return days;
}

const  tableau = document.getElementById('tableau');
var i = 6
var j = i
alert(listDates)
for (d in listDates) {

    if( i == 6) {
        j=i;
        i=0;
        tableau.insertAdjacentHTML('afterend', '<div style="height: 50px" class="row" id="row_"' + i + ' ></div>');
        };

    var element = document.getElementById("row_"+j);
    element.insertAdjacentHTML('afterend', '<div "col-md-1" id="jour">d</div>');
    i=i+1;


    var getDaysOfMonth = function(year, month) {
          var monthDate = moment(year+'-'+month, 'YYYY-MM');
          var daysInMonth = monthDate.daysInMonth();
          var arrDays = [];


          while(daysInMonth) {
            var current = moment().date(daysInMonth);
            arrDays.push(current.format('MM-DD-YYYY'));
            daysInMonth--;
          }
          return arrDays;

    };


    var dateList = getDaysOfMonth(today.getFullYear(), today.getMonth());

    console.log(dateList);