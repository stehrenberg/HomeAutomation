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

            $scope.createUser = function () {
                var dialogScope = $scope.$new(true);
                dialogService.open({
                    template: 'views/dialogs/user.html',
                    controller: 'CreateUserCtrl',
                    scope: dialogScope,
                    preCloseCallback: function (created) {
                        if (created) {
                            bindUsers();
                        }
                    }
                });
            };

            $scope.updateUser = function (user) {
                var dialogScope = $scope.$new(true);
                dialogScope.user = angular.copy(user);
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
