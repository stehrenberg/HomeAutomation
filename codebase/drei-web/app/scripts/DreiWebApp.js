'use strict';

/**
 * @ngdoc overview
 * @name DreiWebApp
 * @description
 * # DreiWebApp
 *
 * Main module of the application.
 */
angular
    .module('DreiWebApp', [
        'ngResource',
        'ngRoute',
        'ngDialog'
    ])
    .constant('AppConfig', {
        serverAddress: 'http://127.0.0.1:8080/'//configured auto
    })
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/dashboard.html',
                controller: 'DashboardCtrl'
            })
            .when('/users', {
                templateUrl: 'views/users.html',
                controller: 'UsersCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });
