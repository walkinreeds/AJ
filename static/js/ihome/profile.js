function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$('#form-name').submit(function () {
    $('.error-msg').hide()
    var name = $('#user-name').val()
    $.ajax({
            url:'/user/user/',
            type:'PUT',
            dataType:'json',
            data:{'name': name},
            success:function (data) {
                if(data.code == '200'){

                }else{
                    $('.error-msg').html('<i class="fa fa-exclamation-circle">用户名已存在</i>')
                    $('.error-msg').show()
                }
            },
            error:function (data) {
                alert('请求失败')

            }
        })
        return false;


})








$(document).ready(function(){

    // $('input[type="file"]').on('change',doUpload)
    // function doUpload() {
    //     var file = this.files[0]
    //     var formData = new FormData($("form-avatar")[0]);
    //     $.ajax({
    //         url:'/user/submit/',
    //         type:'POST',
    //         data:formData,
    //         dataType:'json',
    //         async:false,
    //         cache:false,
    //         contentType:false,
    //         processData:false,
    //         success:function (data) {
    //             if(data.code=='200'){
    //                 location.href='/user/profile/'
    //             }
    //
    //         },
    //         error:function (data) {
    //             console.log(data)
    //             alert(data)
    //         }
    //
    //     })
    //
    // }

    $('#form-avatar').submit(function () {

        $(this).ajaxSubmit({
            url:'/user/user/',
            type:'PUT',
            dataType:'json',
            success:function (data) {
                if(data.code == '200'){
                    $('#user-avatar').attr('src', data.url)
                }
            },
            error:function (data) {
                console.log(data)
                alert('上传图片失败')

            }
        })
        return false;
    })

})







