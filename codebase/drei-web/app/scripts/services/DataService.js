(function () {
    'use strict';

    /**
     * @ngdoc function
     * @name DreiWebApp.service:DataService
     * @description
     * # DataService
     * Service that retrieves and sends data to the backend
     */
    angular.module('DreiWebApp')
        .service('DataService', [
            '$resource',
            'AppConfig',
            function ($resource, appConfig) {

                /**
                 * Create the service with the specified url and parameters.
                 */
                return {
                    getUsers: function () {
                        return $resource(appConfig.serverAddress + '/api/users', {}, {}).query().$promise.then(function (users) {
                            // Transform the user objects in simple user objects.
                            var mappedUsers = [];
                            users.forEach(function (user) {
                                mappedUsers.push({
                                    mac: user.mac,
                                    name: user.name,
                                    sound: user.sound,
                                    light_color: user.light_color
                                });
                            });
                            return mappedUsers;
                        });
                    },
                    createUser: function (user) {
                        return $resource(appConfig.serverAddress + '/api/users', {}, {
                            post: {method: 'POST'}
                        }).post(user).$promise;
                    },
                    deleteUser: function (user) {
                        return $resource(appConfig.serverAddress + '/api/users/' + user.mac, {}, {}).delete().$promise;
                    },
                    updateUser: function (user) {
                        return $resource(appConfig.serverAddress + '/api/users/' + user.mac, {}, {
                            put: {method: 'PUT'}
                        }).put(user).$promise;
                    }
                };

            }
        ]);
}());
