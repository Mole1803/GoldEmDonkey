from Backend.Injector.DependencyInjector import DependencyInjector


class BaseController:
    dependencies: DependencyInjector = None

    @staticmethod
    def set_dependencies(dependency_injector: DependencyInjector):
        BaseController.dependencies = dependency_injector
