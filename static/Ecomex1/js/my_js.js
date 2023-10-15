var temp_button_text;

function CustomFormSubmitPost(e){
    var el = $(e);
    temp_button_text = el.text()
    el.attr('disabled', 'disabled').text("").append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...');
};

function CustomFormSubmitResponse(e){
    var el = $(e);
    el.removeAttr('disabled').text(temp_button_text);
};

var imagecomment = function () {

        var form = $('#commentform');
        form.submit(function(event){
            alert("submit");
            event.preventDefault();
            CustomFormSubmitPost($('#commentform button[type=submit]'));

            var formdata = form.serialize()
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
            })
            .done(function(response){
              if (response == "ok") {
              $('#image-btn').removeAttr("disabled").click()
             }
             })
            .fail(function(){
               console.log("failed");
                })
        })
    };
