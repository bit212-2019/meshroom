__version__ = "2.0"

from meshroom.core import desc


class ExportAnimatedCamera(desc.CommandLineNode):
    commandLine = 'aliceVision_exportAnimatedCamera {allParams}'

    documentation = '''
Convert cameras from an SfM scene into an animated cameras in Alembic file format.
Based on the input image filenames, it will recognize the input video sequence to create an animated camera.
'''

    inputs = [
        desc.File(
            name='input',
            label='Input SfMData',
            description='SfMData file containing a complete SfM.',
            value='',
            uid=[0],
        ),
        desc.File(
            name='viewFilter',
            label='SfMData Filter',
            description='A SfMData file use as filter.',
            value='',
            uid=[0],
        ),
        desc.BoolParam(
            name='exportUVMaps',
            label='Export UV Maps',
            description='Export UV Maps, absolutes values (x,y) of distortion are encoding in  UV channels.',
            value=True,
            uid=[0],
        ),
        desc.BoolParam(
            name='exportUndistortedImages',
            label='Export Undistorted Images',
            description='Export Undistorted Images.',
            value=False,
            uid=[0],
        ),
        desc.BoolParam(
            name='exportFullROD',
            label='Export Full ROD',
            description='Export Full ROD.',
            value=False,
            uid=[0],
        ),
        desc.BoolParam(
            name='correctPrincipalPoint',
            label='Correct Principal Point ',
            description='Correct Principal Point.',
            value=True,
            uid=[0],
        ),
       desc.ChoiceParam(
            name='undistortedImageType',
            label='Undistort Image Format ',
            description='Image file format to use for undistorted images ("jpg", "png", "tif", "exr (half)").',
            value= lambda node: 'jpg' or 'exr' and not node.exportFullROD,
            values=['jpg', 'png', 'tif', 'exr'],
            exclusive=True,
            uid=[0],
            enabled= lambda node: node.exportUndistortedImages.value == 1,
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='Verbosity level (fatal, error, warning, info, debug, trace).',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name='output',
            label='Output filepath',
            description='Output filepath for the alembic animated camera.',
            value=desc.Node.internalFolder,
            uid=[],
        ),
        desc.File(
            name='outputCamera',
            label='Output Camera Filepath',
            description='Output filename for the alembic animated camera.',
            value=desc.Node.internalFolder + 'camera.abc',
            group='',  # exclude from command line
            uid=[],
        ),
        ]
    prev = False
    @classmethod
    def update(cls, node):
        if not isinstance(node.nodeDesc, cls):
            raise ValueError("Node {} is not an instance of type {}".format(node, cls))
            # TODO: use Node version for this test

        if not cls.prev:
            node.undistortedImageType.value = 'jpg'
            cls.prev = True

        if node.exportFullROD.value:
            node.undistortedImageType.value = 'exr'
            node.undistortedImageType.enabled = False
        else:
            node.undistortedImageType.enabled = True

        if not node.exportUndistortedImages.value:
            node.exportFullROD.value = False
