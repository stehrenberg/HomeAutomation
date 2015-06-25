'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:UpdateUserCtrl
 * @description
 * # ErrorCtrl
 * Controller of the dreiWebApp. Responsible for the view which displays a error.
 */
angular.module('DreiWebApp')
    .controller('ErrorCtrl', [
        '$scope',
        function ($scope) {

            /**
             * Closes this dialog.
             */
            $scope.close = function () {
                $scope.closeThisDialog(false);
            };
        }
    ]
);
