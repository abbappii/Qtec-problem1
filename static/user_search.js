<script>
        $('.content').on('click',function(){
            $.ajax({
                url: $('content').data('url'),
                type: 'GET',
                dataType: 'json',
                success: function(resp){
                    $(".content").html(resp);
                },
                error: function(resp){
                    console.log('something went wrong')
                }
            })
        });
</script>