$(function(){
    // 页面后退刷新
    var e=$("#refreshed");
    if(e.val()=="no") {
        e.val('yes');
    }else{
        e.val('no');
　　　　 location.reload();
    }
});

$(function () {

    // 如果用户未登录，显示欢迎您，用户名；否则就显示，欢迎您，请登录;
    if(user === " "){
        var login = $("font").wrap($("<a href='/shopping/login/'></a>").css({color: "red"}).text("请登录"));
        $(".head-span .welcome font").replaceWith(login);
        // 修改购物车的a标签链接，如果未登录，点击时跳转到登录页
        $(".head-span a:eq(1)").attr({href: "/shopping/login/"});

        // 退出登录的标签不触发默认行为
        $(".head-span a:last").on("click",function () {return false})

    }else {
        // 如果用户登录，要显示用户的购物车
        var login = $("font").wrap($("<a href='javascript:;'></a>").css({color: "blue"}).text(user.username));
        $(".head-span .welcome font").replaceWith(login);
        // 修改购物车的a标签链接，如果已登录，直接进入购物车
        $(".head-span a:eq(1)").attr({href: "/shopping/shopping_purchase/"});
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: '/shopping/shopping_car_history/',
            success: function (data) {
                // 请求成功，拿到购物车里的商品添加计数，显示到 '购物车0'上
                $(".head-span a:eq(1) span").text(data);
            }
        });
        // 在点击进入购物车页面时先用ajax发送缓存的异步数据，后台收到缓存的数据后添加到用户的购物车里
        // 完成后返回给前段一个信号，此时开始跳转到a标签的页面中，后台收到url后返回一个页面。
        // 这里有个bug，即异步存数据和取数据的问题。
        $(".head-span a:eq(1)").on("click", function () {
            $.ajax({
                type: "POST",
                dataType: "json",
                data: {"car": $.cookie("car")},
                url: '/shopping/shopping_car/',
                success: function (msg) {
                    // 未操作
                }
            });
            $.removeCookie("car");  // 清除缓存
            return true;
        })
    }

    // 鼠标双击，获取a标签对应的商品名称，显示到下面，提示用户输入购买数量
    $(".goods .good-display a").dblclick(function () {
        // 清空子元素
        $(".good-count").empty();
        var span = $(this).children()[1];

        // 插入第一个提示已选择的商品的span
        var inner = "<span>您已选择<font class='first'>【name】</font>。</span>".replace(/name/, $(span).text());
        $(inner).addClass("good-selected").appendTo(".good-count");

        // 插入第二个提示购买数量的span
        var input = "<span>请输入购买数量<font class='second'>-</font><input name='number' value=1 type='text'/><font class='second'>+</font></span>";
        $(input).addClass("good-selected").appendTo(".good-count");

        // 给"-"添加事件，让它对数量自动减1
        $(".second:first").on("click", function () {
            var value = $(".good-selected input").val();
            if(parseInt(value) >= 1){
                $(".good-selected input").attr({value: parseInt(value)-1});
                if(parseInt(value)-1 === 0){
                    $(this).css({color:"#cccccc"});
                }else {
                    $(this).css({color: "#3c3c3c"});
                }
            }
        });
        // 给"+"添加事件，让它对数量自动加1
        $(".second:last").on("click", function () {
            var value = $(".good-selected input").val();
            $(".good-selected input").attr({value: parseInt(value)+1});
            $(this).css({color: "#3c3c3c"});
            $($(".second:first")).css({color: "#3c3c3c"});
        });
        // 给input添加事件，让它对输入的内容进行数字验证
        $(".good-selected input").blur(function () {
            // 对input的内容进行数字验证
            if(this.value.length==1){
                this.value=this.value.replace(/[^1-9]/g,'')
            }else{
                this.value=this.value.replace(/\D/g,'')
            }
        });


        // 插入第三个加入购物车的a标签，给a标签添加一个事件，将购买商品及数量的信息存到'购物车'
        $(".good-count").append($("<a href='javascript:;'>加入购物车</a>").on("click", function () {
            var good_name = $(span).text(); // 获取第一个span标签内的商品名称
            var good_count = parseInt($(".good-selected input").val()); // 获取购买数量

            if(user === " "){
                alert("请您先登录!")
            }else {
                if(parseInt($(".good-selected input").val()) >= 1){
                    // 缓存购物车car
                    $.cookie("car", $.cookie("car") + "," + good_name + "-" + good_count);
                    // 在购物车那个提示上更新数量
                    var time = $(".head-span a:eq(1) span").text();  // 获取购买次数
                    $(".head-span a:eq(1) span").text(parseInt(time) + 1);
                }
            }
        }));
    });
    // 点击退出，登出当前用户
    $(".head-span a:last").on("click", function () {
        $.removeCookie("car");
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: '/shopping/logout/',
            success: function (msg) {
                console.log(typeof msg, msg);
                if(parseInt(msg) === 1){
                    window.location.href = "/shopping/login/"
                }
            }
        })
    })

});
