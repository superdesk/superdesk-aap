var ngtemplates = require('superdesk-core/tasks/options/ngtemplates.js');
var genApps = ngtemplates['gen-apps'];
var path = require('path');

// get the superdesk.config.js configuration object
function getConfig() {
    return require(path.join(process.cwd(), 'superdesk.config.js'))();
}

// this function overrides the bootstrap of superdesk-client-core
// so that aap specific templates apps can be loaded.
function bootstrapGenApps() {
    // get apps defined in config
    var paths = getConfig().importApps || [];

    if (!paths.length) {
        return 'export default [];\r\n';
    }

    let abs = (p) => {

        if (p === 'aap') {
            return path.join(process.cwd(), p);
        }
        return path.join(process.cwd(), 'node_modules', p);
    };

    let data = 'export default [\r\n\trequire("' + abs(paths[0]) + '").default.name';

    for (var i = 1; i < paths.length; i++) {
        data += ',\r\n\trequire("' + abs(paths[i]) + '").default.name';
    }

    return data + '\r\n];\r\n';
}

genApps.options.bootstrap = bootstrapGenApps;
module.exports = require('superdesk-core/Gruntfile');
