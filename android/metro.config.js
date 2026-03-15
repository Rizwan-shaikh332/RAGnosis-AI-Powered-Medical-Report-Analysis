const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;

const config = getDefaultConfig(projectRoot);

// Ensure Metro only looks in the android/ folder, not the parent workspace
config.watchFolders = [projectRoot];

// Explicitly block the parent node_modules from being resolved
config.resolver.nodeModulesPaths = [
    path.resolve(projectRoot, 'node_modules'),
];

module.exports = config;
