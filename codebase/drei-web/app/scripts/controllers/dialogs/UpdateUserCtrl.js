'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:UpdateUserCtrl
 * @description
 * # UpdateUserCtrl
 * Controller of the dreiWebApp. Responsible for the view which updates a user.
 */
angular.module('DreiWebApp')
    .controller('UpdateUserCtrl', [
        '$scope',
        'DataService',
        function ($scope, dataService) {

            /**
             * @type {boolean} Indicates whether the application is busy.
             */
            $scope.updating = true;

            /**
             * Adds a list of sounds to the scope.
             */
            dataService.getSounds().then(function (sounds) {
                $scope.sounds = sounds;
            });

            /**
             * Closes this dialog.
             */
            $scope.cancel = function () {
                $scope.closeThisDialog(false);
            };

            /**
             * Saves the current user object via a call to the REST api.
             */
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
