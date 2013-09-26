'use strict';

/* Controllers */

function LoginCtrl($scope, $location, User) {
    $scope.login = function(){
        var user = {
            username: $scope.username,
            passwd: $scope.passwd
        };

        User.login(user, function(err, data) {
            if (err) {
                $scope.err = err;
            } else {
                $location.path('/main')
            }
        });
    }
};

function RegisterCtrl($scope, $location, User) {
    $scope.register = function(){
        var user = {
            email: $scope.email,
            passwd: $scope.passwd,
            repasswd: $scope.repasswd,
            username: $scope.username
        };
        if (user.passwd != user.repasswd) {
            $scope.notmatch = true;
        } else {
            User.register(user, function(err, data) {
                if (err){
                    $scope.err = err;
                } else {
                    $location.path('/login');
                }
            });
        }
    };
};

function MainCtrl($scope, $location, User, Container) {
    $scope.user = {};
    $scope.containers = [];
    $scope.images = images;
    $scope.image = images[0];
    User.me(function(err, data) {
        if (err) {
            $location.path('/login');
        } else {
            $scope.user = data;
        }
    });
    User.containers(function(err, data) {
        if (data) {
            $scope.containers = data;
            $scope.containers.forEach(function(container){
                if (!container.passwd) {
                    var index = $scope.containers.indexOf(container);
                    Container.get_passwd(container.container_id, function(err, data) {
                        if (data) {
                            $scope.containers[index].passwd = data;
                        }
                    });
                }
            });
        }
    });
    // Container.images(function(err, data){
    //     if (data) {
    //         $scope.images = data;
    //         $scope.image = "lupino/ubuntu";
    //     }
    // });
    $scope.show = function(elem) {
        console.log(elem);
    };
    $scope.create_container = function() {
        User.create_container($scope.image.image_id, function(err, data) {
            if (data) {
                $scope.containers.push(data);
                if (!data.passwd) {
                    var index = $scope.containers.indexOf(data);
                    Container.get_passwd(data.container_id, function(err, data) {
                        if (data) {
                            $scope.containers[index].passwd = data;
                        }
                    });
                }
            }
        });
    };
    $scope.stop = function(container_id) {
        Container.stop(container_id, function(err, data) {
            console.log(err, data)
        });
    };
    $scope.remove = function(container_id) {
        User.remove_container(container_id, function(err, data) {
            $scope.containers = $scope.containers.filter(function(container) {
                return container.container_id !== container_id
            });
            console.log(err, data)
        });
    };
}
