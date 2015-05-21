'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:CreateUserCtrl
 * @description
 * # CreateUserCtrl
 * Controller of the dreiWebApp
 */
angular.module('DreiWebApp')
    .controller('CreateUserCtrl', [
        '$scope',
        'DataService',
        function ($scope, dataService) {

            $scope.updating = false;

            $scope.user = {};

            dataService.getSounds().then(function (sounds) {
                $scope.sounds = sounds;
                $scope.user.sound = sounds[0];
            });

            $scope.cancel = function () {
                $scope.closeThisDialog(false);
            };

            $scope.save = function () {
                // Check if the form is valid
                if ($scope.userForm.$valid) {
                    var user = $scope.user;
                    dataService.createUser(user).then(function (answer) {
                        var created = answer.created;
                        $scope.closeThisDialog(created);
                    });
                }
            };
        }
    ]
);
