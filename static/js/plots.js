

$("#btnregsubmit").click(function(){
	debugger;
	var uname=document.getElementById('uname').value;
	var name=document.getElementById('name').value;
	var pswd=document.getElementById('pswd').value;
	var email=document.getElementById('email').value;
	var phone=document.getElementById('phone').value;
	var addr=document.getElementById('addr').value;
	
	
	
	//var gender="";
	//if(document.getElementById('gen').checked==true)
	//	gender="Male";
	//if(document.getElementById('gen1').checked==true)
	//	gender="Female";
	
	/* window.location='regdata?uname='+uname+'&name='+name+'&pswd='+pswd+'&email='+email+'&phone='+phone+'&addr='+addr;*/
	
	$.ajax({
            type: 'GET',
            url: '/regdata',
			
        contentType: 'application/json;charset=UTF-8',
            data: {
            'uname': uname,
            'name': name,
            'email': email,
            'phone': phone,
            'pswd': pswd,
            'addr': addr
			

        },
            
        dataType:"json",
            success: function(data) {
				alert('Data saved Successfully');
				acheck();
              // window.location='register';
            },
        });
	
});

$("#btnplancluster").click(function(){
	debugger;
	var ven=document.getElementById('venclus').value;
	
	
	window.location='/gencluster?ven='+ven;
});


$("#btnrideforecast").click(function(){
	debugger;
	var ven=document.getElementById('venfor').value;
	
	
	window.location='/genforecast?ven='+ven;
});

$("#btnpredict").click(function(){
	debugger;
	var loc=document.getElementById('item').value;
	
	
	window.location='/locdata?loc='+loc;
	
	//var gender="";
	//if(document.getElementById('gen').checked==true)
	//	gender="Male";
	//if(document.getElementById('gen1').checked==true)
	//	gender="Female";
	
	/* window.location='regdata?uname='+uname+'&name='+name+'&pswd='+pswd+'&email='+email+'&phone='+phone+'&addr='+addr;*/
	
/*	$.ajax({
            type: 'GET',
            url: '/locdata',
			
        contentType: 'application/json;charset=UTF-8',
            data: {
            'loc': loc	

        },
            
        dataType:"json",
            success: function(data) {
				alert('Data saved Successfully');
				acheck();
              // window.location='register';
            },
        });*/
	
});



$("#btnforgotpassword").click(function(){
	debugger;
	var email=document.getElementById('email').value;
	
	
	$.ajax({
            type: 'GET',
            url: '/fpassword',
			
        contentType: 'application/json;charset=UTF-8',
            data: {
            'email': email
                },
            
        dataType:"json",
            success: function(data) {
					alert('Mail Sent Successfully');
				   window.location='forgotpassword';
            },
			 error: function(data) {
               
            }
        });
	
});



$("#btnlogsubmit").click(function(){
	debugger;
	var email=document.getElementById('email').value;
	var pswd=document.getElementById('pswd').value;
	
	if(email=="admin@gmail.com" && pswd=="admin")
    {
        window.location="adminhome"
    }
    else{
	$.ajax({
            type: 'GET',
            url: '/logdata',
			
        contentType: 'application/json;charset=UTF-8',
            data: {
            'email': email,
            'pswd': pswd
			

        },
            
        dataType:"json",
            success: function(data) {
				if(data=="Failure")
				{
					alert("Credentials not found");
					window.location='register';
				}
				if(data=="Success")
				{
					alert('Logged in Successfully');
				   window.location='dashboard';
				}
            },
			 error: function(data) {
               
            }
        });
    }
	
});

function acheck()
{
	debugger;
}



$("#dataload_btnsubmit").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Data stored successfully');
            },
        });
});

$("#dataload_btnclear").click(function(){
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/cleardataset',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Dataset has been cleared');
            },
        });
});
