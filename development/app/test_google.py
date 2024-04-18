from pytest import mark

from api.v1.object.google import handle_google_response

GOOGLE_RESPONSE_OKAY = {
    'responses': [
        {
            'labelAnnotations': [
                {
                    'mid': '/m/0199g',
                    'description': 'Bicycle',
                    'score': 0.9825226,
                    'topicality': 0.9825226,
                },
                {
                    'mid': '/m/083wq',
                    'description': 'Wheel',
                    'score': 0.97521895,
                    'topicality': 0.97521895,
                },
                {
                    'mid': '/m/0h9mv',
                    'description': 'Tire',
                    'score': 0.97497916,
                    'topicality': 0.97497916,
                },
            ],
            'localizedObjectAnnotations': [
                {
                    'mid': '/m/01bqk0',
                    'name': 'Bicycle wheel',
                    'score': 0.9423431,
                    'boundingPoly': {
                        'normalizedVertices': [
                            {'x': 0.31524897, 'y': 0.78658724},
                            {'x': 0.44186485, 'y': 0.78658724},
                            {'x': 0.44186485, 'y': 0.9692919},
                            {'x': 0.31524897, 'y': 0.9692919},
                        ]
                    },
                },
                {
                    'mid': '/m/01bqk0',
                    'name': 'Bicycle wheel',
                    'score': 0.9337022,
                    'boundingPoly': {
                        'normalizedVertices': [
                            {'x': 0.50342137, 'y': 0.7553652},
                            {'x': 0.6289583, 'y': 0.7553652},
                            {'x': 0.6289583, 'y': 0.9428141},
                            {'x': 0.50342137, 'y': 0.9428141},
                        ]
                    },
                },
                {
                    'mid': '/m/0199g',
                    'name': 'Bicycle',
                    'score': 0.8973106,
                    'boundingPoly': {
                        'normalizedVertices': [
                            {'x': 0.31594256, 'y': 0.66489404},
                            {'x': 0.63338375, 'y': 0.66489404},
                            {'x': 0.63338375, 'y': 0.9687162},
                            {'x': 0.31594256, 'y': 0.9687162},
                        ]
                    },
                },
            ],
        }
    ]
}

EXPECTED_OKAY = {
    'data': {
        'objects': [
            {
                'labelAnnotations': [
                    {
                        'mid': '/m/0199g',
                        'description': 'Bicycle',
                        'score': 0.9825226,
                        'topicality': 0.9825226,
                    },
                    {
                        'mid': '/m/083wq',
                        'description': 'Wheel',
                        'score': 0.97521895,
                        'topicality': 0.97521895,
                    },
                    {
                        'mid': '/m/0h9mv',
                        'description': 'Tire',
                        'score': 0.97497916,
                        'topicality': 0.97497916,
                    },
                ],
                'localizedObjectAnnotations': [
                    {
                        'mid': '/m/01bqk0',
                        'name': 'Bicycle wheel',
                        'score': 0.9423431,
                        'boundingPoly': {
                            'normalizedVertices': [
                                {'x': 0.31524897, 'y': 0.78658724},
                                {'x': 0.44186485, 'y': 0.78658724},
                                {'x': 0.44186485, 'y': 0.9692919},
                                {'x': 0.31524897, 'y': 0.9692919},
                            ]
                        },
                    },
                ],
            }
        ]
    },
    'error': [],
}


GOOGLE_RESPONSE_ERROR = {
    'responses': [
        {
            'error': {
                'code': 3,
                'message': 'The URL does not appear to be accessible by us. Please double check or download the content and pass it in.',
            }
        }
    ]
}

EXPECTED_ERROR = {
    'data': {'objects': []},
    'error': [
        {
            'error': {
                'code': 3,
                'message': 'The URL does not appear to be accessible by us. Please double check or download the content and pass it in.',
            }
        }
    ],
}


@mark.parametrize(
    'given, expected',
    [
        (GOOGLE_RESPONSE_ERROR, EXPECTED_ERROR),
        (GOOGLE_RESPONSE_OKAY, EXPECTED_OKAY),
    ],
)
def test_responses(given: dict, expected: dict) -> None:
    result = {}
    result['data'] = {'objects': []}
    result['error'] = []
    assert handle_google_response(given, result, 0.94) == expected
