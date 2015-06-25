'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the dreiWebApp. Responsible for the dashboard view.
 */
angular.module('DreiWebApp')
    .controller('DashboardCtrl', [
        '$scope',
        'WebsocketService',
        function ($scope, websocketService) {

            /**
             * Listens for refresh messages.
             */
            $scope.$on('ActiveUsersNotification', function (event, activeUsers) {
                $scope.activeUsers = activeUsers;
                $scope.lastUpdated = Date.now();
                $scope.$digest();
            });

            // Force a refresh to retrieve the list of active users.
            websocketService.refreshActiveUsers();
        }
    ]
);
