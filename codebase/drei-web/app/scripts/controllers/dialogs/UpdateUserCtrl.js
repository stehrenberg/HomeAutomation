'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:UpdateUserCtrl
 * @description
 * # UpdateUserCtrl
 * Controller of the dreiWebApp
 */
angular.module('DreiWebApp')
    .controller('UpdateUserCtrl', [
        '$scope',
        'DataService',
        function ($scope, dataService) {

            $scope.cancel = function () {
                $scope.closeThisDialog(false);
            };

            $scope.save = function () {
                // Check if the form is valid
                if ($scope.userForm.$valid) {
                    var user = $scope.user;
                    dataService.updateUser(user).then(function (answer) {
                        var updated = answer.updated;
                        $scope.closeThisDialog(updated);
                    });
                }
            };
        }
    ]
);
