'use strict';

/**
 * @ngdoc function
 * @name DreiWebApp.controller:LatencyCtrl
 * @description
 * # LatencyCtrl
 * Controller of the dreiWebApp. Responsible for the test view.
 */
angular.module('DreiWebApp')
    .controller('LatencyCtrl', [
        '$scope',
        'WebsocketService',
        function ($scope, websocketService) {

            /**
             * @type {string} Initial color for the color swatch under latency test.
             */
            $scope.latencyColor = 'red';

            /**
             * @type {string} Initial color for the color swatch under performance test.
             */
            $scope.performanceColor = 'black';

            /**
             * @type {number} Counts the messages which were already sent during a performance test.
             */
            $scope.performanceCounter = 0;

            /**
             * @type {number} The initial value of the slider for the latency test.
             */
            $scope.latencyValue = 0;

            /**
             * Changes the color of the swatch under latency test according to latencyValue (slider).
             */
            $scope.changeLatencyColor = function () {
                var value = $scope.latencyValue;
                var color;
                switch (value) {
                    case '1':
                        color = '#00ff00';
                        break;
                    case '2':
                        color = '#0000ff';
                        break;
                    case '3':
                        color = '#00ffff';
                        break;
                    case '4':
                        color = '#ff00ff';
                        break;
                    default:
                        color = '#ff0000';
                }
                $scope.latencyColor = color;
                sendLatencyColor(color);
            };

            /**
             * Starts a performance test.
             */
            $scope.startPerformanceTest = function () {
                $scope.performanceCounter = 0;
                for (var r = 0; r < 256; r+=16) {
                    for (var g = 0; g < 256; g+=16) {
                        for (var b = 0; b < 256; b+=16) {
                            var hex = rgbToHex(r, g, b);
                            performanceTestIteration(hex, r+g+b);
                        }
                    }
                }
            };

            /**
             * Makes a single iteration in the performance tests.
             * @param color The color which will be set.
             * @param iteration The current iteration in the performance test.
             */
            function performanceTestIteration(color, iteration) {
                setTimeout(function () {
                    sendLatencyColor(color);
                    $scope.performanceColor = color;
                    $scope.performanceCounter++;
                    $scope.$apply();
                }, iteration * 10);
            }

            /**
             * Calculates the hex value for the specified component.
             * @param c The component whose hex value is calculated.
             * @returns {string} The hex value for the specified component.
             */
            function componentToHex(c) {
                var hex = c.toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }

            /**
             * Transforms a rgb color to a hex color.
             * @param r Red component.
             * @param g Green component.
             * @param b Blue component.
             * @returns {string} A hex string for the specified rgb color.
             */
            function rgbToHex(r, g, b) {
                return '#' + componentToHex(r) + componentToHex(g) + componentToHex(b);
            }

            /**
             * Sends a color request to the server.
             * @param color The color which will be send to the server.
             */
            function sendLatencyColor(color) {
                websocketService.sendLatencyColor(color);
            }
        }
    ]
);
