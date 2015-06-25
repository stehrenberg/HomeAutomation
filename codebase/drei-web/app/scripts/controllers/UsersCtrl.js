'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:UsersCtrl
 * @description
 * # UsersCtrl
 * Controller of the dreiWebApp. Responsible for the user view.
 */
angular.module('DreiWebApp')
    .controller('UsersCtrl', [
        '$scope',
        'DataService',
        'ngDialog',
        function ($scope, dataService, dialogService) {

            /**
             * Binds all available users to the view.
             */
            function bindUsers() {
                dataService.getUsers().then(function (users) {
                    $scope.users = users;
                });
            }

            /**
             * Deletes the specified user.
             * @param user The user which will be deleted.
             */
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

            /**
             * Opens the create user view.
             */
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

            /**
             * Opens the update user view with the specified user object.
             * @param user The user who will be updated.
             */
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
