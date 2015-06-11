(function () {
    'use strict';

    /**
     * @ngdoc factory
     * @name MailApp.factory:$exceptionHandler
     * @description
     * # $exceptionHandler
     * Handler that is responsible for the global error handling.
     */
    angular.module('DreiWebApp')
        .factory('$exceptionHandler', [
            '$injector',
            function ($injector) {

                /**
                 * This function is called when a error occurs. It takes the exception and the cause and opens
                 * the error dialog.
                 */
                return function (error) {
                    var $rootScope = $injector.get('$rootScope');
                    var dialogService = $injector.get('ngDialog');

                    var dialogScope = $rootScope.$new(true);
                    if(error.isCustomError !== undefined && error.isCustomError === true) {
                        dialogScope.errorHeader = error.error;
                        dialogScope.errorMessage = error.errorMessage;
                    } else {
                        dialogScope.errorHeader = 'Fehler: ' + error.message;
                        dialogScope.errorMessage = error.stack;
                    }

                    dialogService.open({
                        template: 'views/dialogs/error.html',
                        controller: 'ErrorCtrl',
                        scope: dialogScope
                    });
                };
            }]
    );
}());
