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
