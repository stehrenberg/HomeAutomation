'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:UsersCtrl
 * @description
 * # UsersCtrl
 * Controller of the dreiWebApp
 */
angular.module('DreiWebApp')
    .controller('UsersCtrl', [
        '$scope',
        'DataService',
        'ngDialog',
        function ($scope, dataService, dialogService) {

            function bindUsers() {
                dataService.getUsers().then(function (users) {
                    $scope.users = users;
                });
            }

            $scope.deleteUser = function (user) {
                dataService.deleteUser(user).then(function (success) {
                    if (success) {
                        bindUsers();
                        console.log('User removed');
                    } else {
                        console.log('ERROR: couldn\'t delete user');
                    }
                });
            };

            $scope.saveUser = function (user) {
                var dialogScope = $scope.$new(true);
                if (user) {
                    dialogScope.user = user;
                } else {
                    dialogScope.user = {};
                }
                dialogService.open({
                    template: 'views/dialogs/user.html',
                    controller: 'UpdateUserCtrl',
                    scope: dialogScope,
                    preCloseCallback: function (updated) {
                        if (updated) {
                            bindUsers();
                        }
                    }
                });
            };

            // INIT
            bindUsers();
        }
    ]
);
