'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.directive:isActiveNav
 * @description
 * # isActiveNav
 * Directive which is responsible for marking menu entries as inactive/active.
 */
angular.module('DreiWebApp')
    .directive('isActiveNav', ['$location', function ($location) {
        return {
            restrict: 'A',
            link: function (scope, element) {
                scope.location = $location;
                scope.$watch('location.path()', function (currentPath) {
                    if ('/#' + currentPath === element[0].attributes['href'].nodeValue) {
                        element.parent().addClass('active');
                    } else {
                        element.parent().removeClass('active');
                    }
                });
            }
        };
    }]);