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

                function broadcastNotification(data) {
                    $rootScope.$broadcast('ActiveUsersNotification', data);
                }

                function initWebsocket() {
                    var socket = io.connect(appConfig.serverAddress);
                    socket.on('connect', function () {
                        socket.emit('ConnectEvent');
                    });
                    socket.on('ActiveUsersNotification', broadcastNotification);
                }

                // Initialize the websocket
                initWebsocket();
            }
        ]);

    /**
     * Initializes the WebsocketService on startup.
     */
    angular.module('DreiWebApp').run(['WebsocketService', function () {
    }]);
}());
