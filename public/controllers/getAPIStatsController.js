var logStats = angular.module('logStats', []);

logStats.controller('mainController', function ($scope, $http) {

    function getDataSet() {
        return [100,200,300,150];
    }
    $scope.logstreamLoading = true;
    $scope.getLogsFromEAPI = function() {
        $scope.logstreamLoading = true;
        var dateFrom = $('#datepicker2').val();
        var dateTo = $('#datepicker3').val();
        console.log(dateFrom, dateTo)
        var startTimeStamp = dateFrom.replace('/','').replace('/','') + "000000";
        var endTimeStamp = dateTo.replace('/','').replace('/','')  + "000000";
        console.log(startTimeStamp, endTimeStamp)
        var endPointUrl = "http://127.0.0.1:5001/logs/date";
        $http.get(endPointUrl + "/" + startTimeStamp + "/" + endTimeStamp)
            .success(function (response) {
                console.dir(response);
                $scope.logstreamLoading = false;
                $scope.logsData = response.data;
                $scope.dateTimeVsCount = response.dateTimeVsCount;


		var ctx = document.getElementById('chart1').getContext('2d');
		ctx.canvas.width = 1000;
		ctx.canvas.height = 300;
		var cfg = {
			type: 'line',
			data: {
				labels: response.dateTimeVsCount['labels'],
				datasets: [{
					label: 'HTTP Requests',
					backgroundColor: window.chartColors.red,
					borderColor: window.chartColors.red,
					data: response.dateTimeVsCount['values'],
					fill: false,
				}]
			},
			options: {
					responsive: true,
				title: {
					display: true,
					text: 'Total Requests vs Date Graph'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Total Requests'
						}
					}]
				}
			}
		};
		var chart = new Chart(ctx, cfg);


            })
            .error(function (response) {
                console.error("Error");
                $scope.logstreamLoading = false;
            });
    }



});
