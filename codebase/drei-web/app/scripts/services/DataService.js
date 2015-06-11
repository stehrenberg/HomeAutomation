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

                function DataError(error, errorMessage) {
                    this.error = error;
                    this.errorMessage = errorMessage;
                    this.isCustomError = true;
                    return this;
                }

                function createDataError(error, message) {
                    var errorText = 'Fehler: ' + error.statusText + ' (' + error.status + ')';
                    return new DataError(errorText, message);
                }

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
                        }).catch(function (error) {
                            var message = 'Konnte Nutzer nicht empfangen. Ist der Server verfügbar!?';
                            throw createDataError(error, message);
                        });
                    },
                    createUser: function (user) {
                        return $resource(appConfig.serverAddress + '/api/users', {}, {
                            post: {method: 'POST'}
                        }).post(user).$promise.catch(function (error) {
                                var message = 'Konnte Nutzer nicht anlegen. Existiert diese Mac-Adresse bereits!?';
                                throw createDataError(error, message);
                            });
                    },
                    deleteUser: function (user) {
                        return $resource(appConfig.serverAddress + '/api/users/' + escape(user.mac), {}, {}).delete().$promise.catch(function () {
                            var message = 'Konnte Nutzer nicht löschen. Existiert ein User mit dieser Mac-Adresse!?';
                            throw createDataError(error, message);
                        });
                    },
                    updateUser: function (user) {
                        return $resource(appConfig.serverAddress + '/api/users/' + escape(user.mac), {}, {
                            put: {method: 'PUT'}
                        }).put(user).$promise.catch(function () {
                                var message = 'Konnte Nutzer nicht bearbeiten. Existiert ein User mit dieser Mac-Adresse!?';
                                throw createDataError(error, message);
                            });
                    },
                    getSounds: function () {
                        return $resource(appConfig.serverAddress + '/api/sounds', {}, {}).query().$promise.catch(function () {
                            var message = 'Konnte Songs nicht empfangen. Ist der Server verfügbar!?';
                            throw createDataError(error, message);
                        });
                    }
                };

            }
        ]);
}());
