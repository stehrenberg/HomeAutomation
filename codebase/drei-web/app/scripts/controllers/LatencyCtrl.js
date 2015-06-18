'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:LatencyCtrl
 * @description
 * # LatencyCtrl
 * Controller of the dreiWebApp
 */
angular.module('DreiWebApp')
    .controller('LatencyCtrl', [
        '$scope',
        'WebsocketService',
        function ($scope, websocketService) {

            $scope.latencyColor = 'red';

            $scope.latencyValue = 0;

            $scope.changeLatencyColor = function () {
                var value = $scope.latencyValue;
                var color;
                switch(value) {
                    case '1':
                        color = '#00ff00';
                        $scope.latencyColor = color;
                        sendLatencyColor(color);
                        break;
                    case '2':
                        color = '#0000ff';
                        $scope.latencyColor = color;
                        sendLatencyColor(color);
                        break;
                    case '3':
                        color = '#00ffff';
                        $scope.latencyColor = color;
                        sendLatencyColor(color);
                        break;
                    case '4':
                        color = '#ff00ff';
                        $scope.latencyColor = color;
                        sendLatencyColor(color);
                        break;
                    default:
                        color  = '#ff0000';
                        $scope.latencyColor = color;
                        sendLatencyColor(color);
                }
            };

            function sendLatencyColor(color) {
                websocketService.sendLatencyColor(color);
            }
        }
    ]
);
