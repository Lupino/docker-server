'use strict';

/* App Module */

angular.module('docker', ['UserServices', 'ContainerServices'])
.config(['$routeProvider', function($routeProvider){
    $routeProvider.
    when('/main', {templateUrl: '/static/partials/main.html', controller: MainCtrl}).
    when('/login', {templateUrl: '/static/partials/login.html', controller: LoginCtrl}).
    when('/register', {templateUrl: '/static/partials/register.html', controller: RegisterCtrl}).
    otherwise({redirectTo: '/main'})
}]);
