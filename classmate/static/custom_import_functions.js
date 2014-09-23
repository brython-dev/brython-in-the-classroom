var $B=__BRYTHON__
function import_py_via_localStorage(module,path,package){
    // import Python module at specified path
    try{
        var file_contents=localStorage[path]
        if (file_contents === undefined) return null
    }catch(err){
        return null
    }
    $B.imported[module.name].$package = module.is_package
    if(path.substr(path.length-12)=='/__init__.py'){
        $B.imported[module.name].__package__ = module.name
    }else if(package!==undefined){
        $B.imported[module.name].__package__ = package
    }else{
        var mod_elts = module.name.split('.')
        mod_elts.pop()
        $B.imported[module.name].__package__ = mod_elts.join('.')
    }
    _json=JSON.parse(file_contents)
    return $B.run_py(module,path, _json.contents)
  }

function import_from_localStorage(mod_name, origin, package){
    var module = {name:mod_name,__class__:$B.$ModuleDict}

    mod_path = mod_name.replace(/\./g,'/')
 
    var root
    for (var j=0; j < $B.path.length; j++) {
        if ($B.path[j].substring(0,4) == 'http') continue
        if ($B.path[j].substring(0,10) != '/classmate') {
           if ($B.path[j].substring(0,1) != '/') {
              root='/classmate/'+$B.path[j]
           } else {
              root='/classmate'+$B.path[j]
           }
        } else {
           root=$B.path[j]
        }
        if (root.substring(root.length, 1) == '/') {
           root=root.substring(0,root.length-1)
        }
        var py_paths = [root+'/'+mod_path+'.py',
                        root+'/'+mod_path+'/__init__.py']

        for(var i=0;i<py_paths.length;i++){
           var py_mod = import_py_via_localStorage(module, py_paths[i],package)
           if(py_mod!==null) return true
        }
    }
    return null
}
