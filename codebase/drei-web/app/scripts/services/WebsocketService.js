(function () {
    'use strict';

    /**
     * @ngdoc function
     * @name DreiWebApp.service:WebsocketService
     * @description
     * # WebsocketService
     * Service that retrieves and sends data to the backend via a websocket.
     */
    angular.module('DreiWebApp')
        .service('WebsocketService', [
            '$rootScope',
            'AppConfig',
            function ($rootScope, appConfig) {

                /**
                 * The socket object which holds the connection.
                 */
                var socket;

                /**
                 * Sends the data via a broadcast trough the whole client app.
                 * @param data The data which will be send in the broadcast.
                 */
                function broadcastNotification(data) {
                    $rootScope.$broadcast('ActiveUsersNotification', JSON.parse(data));
                }

                /**
                 * Inits the websocket connection and registers the event handlers.
                 */
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
                    /**
                     * Send a request to the server which forces a resend of the current active users.
                     */
                    refreshActiveUsers: function () {
                        socket.emit('GetActiveUsersEvent');
                    },
                    /**
                     * Send a color request which forces the server to change the light color.
                     * @param color
                     */
                    sendLatencyColor: function(color) {
                        socket.emit('LatencyColorEvent', color);
                    }
                };
            }
        ]);
}());
