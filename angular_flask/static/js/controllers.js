'use strict';

/* Controllers */

function IndexController($scope) {
	
}

function AboutController($scope) {
	
}

function PostListController($scope, Post) {
	var postsQuery = Post.get({}, function(posts) {
		$scope.posts = posts.objects;
	});
}

function DisplayAllController($scope, Restangular) {
    Restangular.setBaseUrl('/api');
    // This function is used to map the JSON data to something Restangular
    // expects
    // add a response intereceptor
    Restangular.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
        var extractedData;
        // .. to look for getList operations
        if (operation === "getList") {
            // .. and handle the data and meta data
            extractedData = data[0].post;
            extractedData.meta = data[0].meta;
        } else {
            extractedData = data.post;
        }
        return extractedData;
    });

    $scope.posts = Restangular.all("posts").getList();
}

function PostDetailController($scope, $routeParams, Post) {
	var postQuery = Post.get({ postId: $routeParams.postId }, function(post) {
		$scope.post = post;
	});
}
