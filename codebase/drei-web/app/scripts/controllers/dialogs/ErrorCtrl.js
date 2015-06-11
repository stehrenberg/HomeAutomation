'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:UpdateUserCtrl
 * @description
 * # UpdateUserCtrl
 * Controller of the dreiWebApp
 */
angular.module('DreiWebApp')
    .controller('ErrorCtrl', [
        '$scope',
        function ($scope) {

            $scope.close = function () {
                $scope.closeThisDialog(false);
            };
        }
    ]
);
