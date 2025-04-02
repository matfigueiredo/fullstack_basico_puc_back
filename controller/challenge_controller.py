from flask import Blueprint, request, jsonify
from repository.challenge_repository import ChallengeRepository

challenge_bp = Blueprint('challenges', __name__)
challenge_repo = ChallengeRepository()

@challenge_bp.route('/challenges', methods=['GET'])
def get_challenges():
    """
    Get all challenges
    ---
    parameters:
      - name: category
        in: query
        type: string
        required: false
        description: Filter challenges by category
    responses:
      200:
        description: List of challenges
      404:
        description: No challenges found
      500:
        description: Internal server error
    """
    try:
        category: str | None = request.args.get('category')
        challenges: list[dict] = challenge_repo.get_all_challenges(category)
        
        if not challenges:
            return jsonify({
                "message": "No challenges found",
                "data": []
            }), 404
            
        return jsonify({
            "message": "Challenges retrieved successfully",
            "data": challenges
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching challenges",
        }), 500

@challenge_bp.route('/challenges', methods=['POST'])
def create_challenge():
    """
    Create a new challenge
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            category:
              type: string
    responses:
      201:
        description: Challenge created
    """
    data = request.get_json()
    title, description, category = data.get('title'), data.get('description'), data.get('category')

    if not title or not description or not category:
        return jsonify({"message": "Missing required fields"}), 400

    challenge_repo.create_challenge(data)
    return jsonify({"message": "Challenge created successfully!"}), 201

@challenge_bp.route('/challenges/weekly', methods=['GET'])
def get_weekly_challenge():
    """
    Get a random challenge
    ---
    responses:  
      200:
        description: Challenge retrieved successfully
      404:
        description: No challenges available
      500:
        description: Internal server error
    """
    try:
        challenge: dict = challenge_repo.get_weekly_challenge()
        
        if not challenge:
            return jsonify({
                "message": "No challenges available",
                "data": None
            }), 404
            
        return jsonify({
            "message": "Challenge retrieved successfully",
            "data": challenge
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching challenge",
            "error": "Internal server error, check server"
        }), 500

@challenge_bp.route('/challenges/<int:challenge_id>', methods=['GET'])
def get_challenge_by_id(challenge_id):
    """
    Get a challenge by ID
    ---
    parameters:
      - name: challenge_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Challenge retrieved successfully
      404:
        description: Challenge not found
      500:
        description: Internal server error
    """
    try:
        challenge: dict = challenge_repo.get_challenge_by_id(challenge_id)
        
        if not challenge:
            return jsonify({
                "message": "Challenge not found",
                "data": None
            }), 404
            
        return jsonify({
            "message": "Challenge retrieved successfully",
            "data": challenge
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "An error occurred while fetching challenge",
            "error": "Internal server error, check server"
        }), 500

@challenge_bp.route('/challenges/<int:challenge_id>', methods=['DELETE'])
def delete_challenge(challenge_id):
    """
    Delete a challenge by ID
    ---
    parameters:
      - name: challenge_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Challenge deleted successfully
      404:
        description: Challenge not found
      500:
        description: Internal server error
    """
    try:
        challenge_repo.delete_challenge(challenge_id)
        return jsonify(), 204
    except Exception as e:
        return jsonify({
            "message": "An error occurred while deleting challenge",
            "error": "Internal server error, check server"
        }), 500
