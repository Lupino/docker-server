'use strict';

/* Services */

function toForm(data) {
    var retval = []
    for(var k in data){
        retval.push(k + '=' + encodeURI(data[k]))
    }
    return retval.join('&')
}

angular.module('UserServices', []).
factory('User', function($http){
    var User =  {

        me: function(callback){
            $http.get('/api/user/me').success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        login: function(user, callback){
            $http.post('/api/user/login', toForm(user)).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        containers: function(callback){
            $http.get('/api/user/containers').success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    data = data.map(function(v){
                        v.createdAt = new Date(v.created_at * 1000).toLocaleString();
                        v.stopAt = new Date(v.stop_at * 1000).toLocaleString();
                        var image = images.filter(function(image){
                            return image.image_id === v.image_id;
                        });
                        if (image.length === 1) {
                            v.image = image[0];
                        }
                        return v;
                    });
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        create_container: function(image, callback){
            $http.post('/api/user/create/container', toForm({image: image})).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    data.createdAt = new Date(data.created_at * 1000).toLocaleString()
                    data.stopAt = new Date(data.stop_at * 1000).toLocaleString()
                    var image = images.filter(function(image){
                        return image.image_id === data.image_id;
                    });
                    if (image.length === 1) {
                        data.image = image[0];
                    }
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        remove_container: function(container_id, callback){
            $http.delete('/api/user/remove/container/' + container_id).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        register: function(user, callback){
            $http.post('/api/user/register', toForm(user)).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        passwd: function(passwd, callback){
            $http.post('/api/user/passwd', toForm(passwd)).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        }
    }

    return User;
});

angular.module('ContainerServices', []).
factory('Container', function($http){
    var Container =  {
        start: function(container_id, callback){
            $http.post('/api/container/start/'+container_id).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        restart: function(container_id, callback){
            $http.post('/api/container/restart/'+container_id).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        stop: function(container_id, callback){
            $http.post('/api/container/stop/'+container_id).success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        images: function(callback){
            $http.get('/api/images').success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        },
        get_passwd: function(container_id, callback){
            $http.get('/api/container/' + container_id +'/passwd').success(function(data, status){
                if (data.err){
                    callback(data.err, null);
                }else{
                    callback(null, data);
                }
            }).error(function(data, status){
                callback(status);
            });
        }
    }

    return Container;
});
