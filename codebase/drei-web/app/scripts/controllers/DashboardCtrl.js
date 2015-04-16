'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the dreiWebApp
 */
angular.module('DreiWebApp')
    .controller('DashboardCtrl', [
        '$scope',
        'DataService',
        function ($scope, dataService) {

            $scope.$on('ActiveUsersNotification', function (event, data) {
                $scope.activeUsers = data;
            });
        }
    ]
);
