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
            $scope.performanceColor = 'black';

            $scope.performanceCounter = 0;

            $scope.latencyValue = 0;

            $scope.changeLatencyColor = function () {
                var value = $scope.latencyValue;
                var color;
                switch (value) {
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
                        color = '#ff0000';
                        $scope.latencyColor = color;
                        sendLatencyColor(color);
                }
            };

            $scope.startPerformanceTest = function () {
                $scope.performanceCounter = 0;
                for (var r = 0; r < 256; r+=16) {
                    for (var g = 0; g < 256; g+=16) {
                        for (var b = 0; b < 256; b+=16) {
                            var hex = rgbToHex(r, g, b);
                            test(hex, r+g+b);
                        }
                    }
                }
            };

            function test(color, iteration) {
                setTimeout(function () {
                    sendLatencyColor(color);
                    $scope.performanceColor = color;
                    $scope.performanceCounter++;
                    $scope.$apply();
                }, iteration * 10);
            }

            function componentToHex(c) {
                var hex = c.toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }

            function rgbToHex(r, g, b) {
                return '#' + componentToHex(r) + componentToHex(g) + componentToHex(b);
            }

            function sendLatencyColor(color) {
                websocketService.sendLatencyColor(color);
            }
        }
    ]
);
