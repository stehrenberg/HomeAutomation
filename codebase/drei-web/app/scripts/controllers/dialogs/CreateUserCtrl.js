'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:CreateUserCtrl
 * @description
 * # CreateUserCtrl
 * Controller of the dreiWebApp. Responsible for the view which creates a user.
 */
angular.module('DreiWebApp')
    .controller('CreateUserCtrl', [
        '$scope',
        'DataService',
        function ($scope, dataService) {

            /**
             * @type {boolean} Indicates whether the application is busy or not.
             */
            $scope.updating = false;

            /**
             * @type {{User}} The current user object which will be saved.
             */
            $scope.user = {};

            /**
             * Adds all sound files to the scope.
             */
            dataService.getSounds().then(function (sounds) {
                $scope.sounds = sounds;
                $scope.user.sound = sounds[0];
            });

            /**
             * Cancels the creation of this user.
             */
            $scope.cancel = function () {
                $scope.closeThisDialog(false);
            };

            /**
             * Saves the current user. Sends a callback against the REST api.
             */
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
