(function () {
    'use strict';

    /**
     * @ngdoc function
     * @name DreiWebApp.service:WebsocketService
     * @description
     * # WebsocketService
     * Service that retrieves and sends data to the backend
     */
    angular.module('DreiWebApp')
        .service('WebsocketService', [
            '$rootScope',
            'AppConfig',
            function ($rootScope, appConfig) {

                var socket;

                function broadcastNotification(data) {
                    $rootScope.$broadcast('ActiveUsersNotification', JSON.parse(data));
                }

                function initWebsocket() {
                    socket = io.connect(appConfig.serverAddress);
                    socket.on('ActiveUsersNotification', broadcastNotification);
                    socket.on('connect', function () {
                        socket.emit('Connected');
                    });
                }

                // Initialize the websocket
                initWebsocket();

                return {
                    refreshActiveUsers: function () {
                        socket.emit('GetActiveUsersEvent');
                    },
                    sendLatencyColor: function(color) {
                        socket.emit('LatencyColorEvent', color);
                    }
                };
            }
        ]);
}());
