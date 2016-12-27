define(['models/commands'],function(commands){
	var instance = null;

    function Modem(){
        if(instance !== null){
            throw new Error("Cannot instantiate more than one Modem, use Modem.getInstance()");
        }

        this.init();
    }

    Modem.prototype = {
        init: function(){
            namespace = '';
            socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

            socket.on('connect', function() {
               console.log('connected');
            });

            socket.on('module_info', function(data) {
               console.log('connected to module: ' + data.uid);
                // TODO
/*               $$('header').setValues({header:"oss7", status:
                       'Connected to ' + data.uid + ' using D7AP v' + data.d7ap_version + ' running app \'' + data.application_name +
                       '\' using git sha1 ' + data.git_sha1}
               )*/
            });

            socket.on('received_alp_command', function(msg) {
                commands.data.add(msg);
            });
        },

        execute_command:function(command, cb) {
            socket.emit('execute_command', command, cb);
        }
    }

    Modem.getInstance = function(){
        if(instance === null){
            instance = new Modem();
        }
        return instance;
    };

	return Modem.getInstance();
});

