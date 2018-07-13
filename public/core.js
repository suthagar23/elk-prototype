var opnFvApp = angular.module('opnFvApp', ['ngRoute', 'logStats']);
// configure the routes
opnFvApp.config(function ($routeProvider) {
    $routeProvider
    // route for the home page
        .when('/', {
            templateUrl: 'index.html',
            controller: 'mainController'
        })
});
