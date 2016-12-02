import luigi
###### Meta class ######
 
class DependencyMetaTask(luigi.Task):
    # METHODS FOR AUTOMATING DEPENDENCY MANAGEMENT
    def requires(self):
        upstream_tasks = []
        for param_val in self.param_args:
            if type(param_val) is dict:
                if 'upstream' in param_val:
                    upstream_tasks.append(param_val['upstream']['task'])
        return upstream_tasks
 
    def get_input(self, input_name):
        param = self.param_kwargs[input_name]
        if type(param) is dict and 'upstream' in param:
            return param['upstream']['task'].output()[param['upstream']['port']]
        else: 
            return param
 
 ###### Normal classes ######

